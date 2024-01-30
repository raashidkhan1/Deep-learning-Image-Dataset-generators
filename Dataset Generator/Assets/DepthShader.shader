Shader "Custom/DepthShader"
{
    Properties
    {
        _NearClipPlane ("Near Clip Plane", Float) = 0.3
        _FarClipPlane ("Far Clip Plane", Float) = 50
    }
    SubShader
    {
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            float _NearClipPlane;
            float _FarClipPlane;

            struct appdata
            {
                float4 vertex : POSITION;
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                float depth : TEXCOORD0;
            };

            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.depth = o.pos.z / o.pos.w;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                // Linearize depth
                float depth = i.depth;
                /*
                depth = depth * 0.5 + 0.5; // Transform to [0, 1] range
                depth = _FarClipPlane / (_FarClipPlane - _NearClipPlane) - depth * _FarClipPlane / (_FarClipPlane - _NearClipPlane);
                */

                // Output the depth as grayscale
                return fixed4(depth, depth, depth, 1.0);
            }
            ENDCG
        }
    }
}
