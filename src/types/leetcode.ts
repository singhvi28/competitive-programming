export interface LeetCodeProblem {
  id: string | number;
  name: string;
  url: string;
  why?: string;
  companies?: string[];
}

export interface LeetCodeCategory {
  id?: number;
  title: string;
  description: string;
  problems: LeetCodeProblem[];
}
