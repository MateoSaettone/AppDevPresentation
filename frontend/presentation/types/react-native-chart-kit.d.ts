// declare module 'react-native-chart-kit' {
//     import { Component } from 'react';
//     import { StyleProp, ViewStyle } from 'react-native';
  
//     interface ChartConfig {
//       backgroundColor: string;
//       backgroundGradientFrom?: string;
//       backgroundGradientTo?: string;
//       decimalPlaces?: number;
//       color: (opacity: number) => string;
//       labelColor: (opacity: number) => string;
//       style?: StyleProp<ViewStyle>;
//       propsForDots?: { [key: string]: string };
//       propsForBackgroundLines?: { [key: string]: string };
//     }
  
//     interface Dataset {
//       data: number[];
//       color?: (opacity: number) => string;
//       strokeWidth?: number;
//     }
  
//     interface LineChartProps {
//       data: {
//         labels: string[];
//         datasets: Dataset[];
//         legend?: string[];
//       };
//       width: number;
//       height: number;
//       chartConfig: ChartConfig;
//       bezier?: boolean;
//       style?: StyleProp<ViewStyle>;
//     }
  
//     export class LineChart extends Component<LineChartProps> {}
//   }
  