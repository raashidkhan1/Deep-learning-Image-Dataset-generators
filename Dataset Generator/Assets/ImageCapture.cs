using System.Collections;
using System.IO;
using UnityEngine;

public class ImageCapture : MonoBehaviour
{
    public Camera captureCamera;
    public int fileCounter = 0;
    public string folderPath;
    public Light sceneLight;
    public Transform target; 
    public Camera depthCamera; // Camera for capturing depth
    public Material depthMaterial; // Material using the depth shader
    public string depthFolderPath;
    private static readonly int NearClipPlane = Shader.PropertyToID("_NearClipPlane");
    private static readonly int FarClipPlane = Shader.PropertyToID("_FarClipPlane");

    private void Start()
    {
        // Ensure the directory exists
        if (!Directory.Exists(folderPath))
        {
            Directory.CreateDirectory(folderPath);
        }
        
        // Initialize Render Texture if not done already
        if (captureCamera.targetTexture == null)
        {
            captureCamera.targetTexture = new RenderTexture(Screen.width, Screen.height, 24);
        }
        
        if (depthCamera.targetTexture == null) {
            depthCamera.targetTexture = new RenderTexture(Screen.width, Screen.height, 24, RenderTextureFormat.Depth);
        }
        depthCamera.depthTextureMode = DepthTextureMode.Depth;
        depthMaterial.SetFloat(NearClipPlane, depthCamera.nearClipPlane);
        depthMaterial.SetFloat(FarClipPlane, depthCamera.farClipPlane);

    }

    private void Update()
    {
        // For example, capture an image each time the 'C' key is pressed
        if (Input.GetKeyDown(KeyCode.C))
        {
            PositionLightRandomly();
            PositionCamera();
            StartCoroutine(CaptureImage());
            StartCoroutine(CaptureDepthImage());
        }
    }
    
    private void PositionLightRandomly()
    {
        // Randomize within 2 meters
        float radius = Random.Range(0.0f, 2.0f);
        float polar = Random.Range(0.0f, Mathf.PI);
        float azimuth = Random.Range(0.0f, 2 * Mathf.PI);

        // Convert spherical coordinates to Cartesian coordinates for 3D space
        Vector3 lightPosition = new Vector3(
            radius * Mathf.Sin(polar) * Mathf.Cos(azimuth),
            radius * Mathf.Sin(polar) * Mathf.Sin(azimuth),
            radius * Mathf.Cos(polar)
        );

        sceneLight.transform.position = lightPosition;
    }
    
    private void PositionCamera()
    {
        // Position camera randomly, yet always looking at the center
        // Similar logic to light positioning can be used, or you can position it based on a specific logic

        // Ensure camera is looking at the target
        var position = target.position;
        captureCamera.transform.LookAt(position);
        depthCamera.transform.LookAt(position);
    }

    private IEnumerator CaptureImage()
    {
        // Wait till the end of the frame to ensure all rendering is done
        yield return new WaitForEndOfFrame();

        RenderTexture renderTexture = captureCamera.targetTexture;

        // Create a temporary texture
        Texture2D renderResult = new Texture2D(renderTexture.width, renderTexture.height, TextureFormat.ARGB32, false);
        Rect rect = new Rect(0, 0, renderTexture.width, renderTexture.height);

        // Render the camera's view
        captureCamera.Render();

        // Read the pixels from the Render Texture
        RenderTexture.active = renderTexture;
        renderResult.ReadPixels(rect, 0, 0);
        renderResult.Apply();

        // Reset the active Render Texture
        RenderTexture.active = null;

        byte[] byteArray = renderResult.EncodeToPNG();
        Destroy(renderResult);

        // Save the image
        File.WriteAllBytes(Path.Combine(folderPath, $"Capture_{fileCounter++}.png"), byteArray);
    }
    
    private IEnumerator CaptureDepthImage()
    {
        // Ensure depth camera settings match the main camera
        var transform1 = captureCamera.transform;
        var transform2 = depthCamera.transform;
        transform2.position = transform1.position;
        transform2.rotation = transform1.rotation;

        // Render the depth view
        depthCamera.RenderWithShader(depthMaterial.shader, "");

        // Wait till the end of the frame
        yield return new WaitForEndOfFrame();

        // Read the pixels from the Render Texture
        RenderTexture.active = depthCamera.targetTexture;
        Texture2D depthResult = new Texture2D(RenderTexture.active.width, RenderTexture.active.height, TextureFormat.RGB24, false);
        depthResult.ReadPixels(new Rect(0, 0, RenderTexture.active.width, RenderTexture.active.height), 0, 0);
        depthResult.Apply();
        RenderTexture.active = null;

        byte[] depthBytes = depthResult.EncodeToPNG();
        Destroy(depthResult);

        // Save the depth image
        File.WriteAllBytes(Path.Combine(depthFolderPath, $"DepthCapture_{fileCounter}.png"), depthBytes);
    }
}
