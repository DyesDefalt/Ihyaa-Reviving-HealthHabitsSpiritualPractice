import React from 'react';
import Svg, { Defs, G, Line, Pattern, Polygon, Rect } from 'react-native-svg';

/** Eight-point khatam star tessellation — the quiet Islamic accent of the app. */
export function GeoPattern({
  color = '#FFFFFF',
  opacity = 0.09,
  size = 56,
}: {
  color?: string;
  opacity?: number;
  size?: number;
}) {
  return (
    <Svg style={{ position: 'absolute', left: 0, right: 0, top: 0, bottom: 0 }} width="100%" height="100%">
      <Defs>
        <Pattern id="khatam" x="0" y="0" width={size} height={size} patternUnits="userSpaceOnUse">
          <G>
            <Polygon
              points={`${size / 2},2 ${size * 0.66},${size * 0.34} ${size - 2},${size / 2} ${size * 0.66},${size * 0.66} ${size / 2},${size - 2} ${size * 0.34},${size * 0.66} 2,${size / 2} ${size * 0.34},${size * 0.34}`}
              fill="none"
              stroke={color}
              strokeWidth={0.8}
              opacity={opacity}
            />
            <Polygon
              points={`${size * 0.28},${size * 0.28} ${size * 0.72},${size * 0.28} ${size * 0.72},${size * 0.72} ${size * 0.28},${size * 0.72}`}
              fill="none"
              stroke={color}
              strokeWidth={0.6}
              opacity={opacity * 0.75}
            />
            <Line x1={0} y1={0} x2={size} y2={size} stroke={color} strokeWidth={0.4} opacity={opacity * 0.4} />
            <Line x1={size} y1={0} x2={0} y2={size} stroke={color} strokeWidth={0.4} opacity={opacity * 0.4} />
          </G>
        </Pattern>
      </Defs>
      <Rect x="0" y="0" width="100%" height="100%" fill="url(#khatam)" />
    </Svg>
  );
}
