export type ContestType = 'Div. 2' | 'Educational' | 'Combined / Global' | string;

export interface VirtualContest {
  id: string;
  name: string;
  url: string;
  type: ContestType;
}
