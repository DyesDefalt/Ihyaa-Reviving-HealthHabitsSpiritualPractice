import React from 'react';
import { View } from 'react-native';
import Svg, { Circle } from 'react-native-svg';

type Ring = { pct: number; color: string };

/** Concentric progress rings — one per pillar. */
export function ProgressRings({
  rings,
  size = 116,
  stroke = 9,
  gap = 4,
  track = 'rgba(255,255,255,0.18)',
  children,
}: {
  rings: Ring[];
  size?: number;
  stroke?: number;
  gap?: number;
  track?: string;
  children?: React.ReactNode;
}) {
  const center = size / 2;
  return (
    <View style={{ width: size, height: size, alignItems: 'center', justifyContent: 'center' }}>
      <Svg width={size} height={size} style={{ position: 'absolute' }}>
        {rings.map((r, i) => {
          const radius = center - stroke / 2 - i * (stroke + gap);
          if (radius <= 2) return null;
          const circ = 2 * Math.PI * radius;
          const pct = Math.max(0, Math.min(100, r.pct));
          return (
            <React.Fragment key={i}>
              <Circle cx={center} cy={center} r={radius} stroke={track} strokeWidth={stroke} fill="none" />
              <Circle
                cx={center}
                cy={center}
                r={radius}
                stroke={r.color}
                strokeWidth={stroke}
                fill="none"
                strokeLinecap="round"
                strokeDasharray={`${circ}`}
                strokeDashoffset={circ * (1 - pct / 100)}
                transform={`rotate(-90 ${center} ${center})`}
              />
            </React.Fragment>
          );
        })}
      </Svg>
      {children}
    </View>
  );
}
