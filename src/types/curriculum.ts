export interface CurriculumProblem {
  id: string;
  name: string;
  contestId: number;
  index: string;
  rating: number;
  url: string;
  technique: string;
  insight: string;
  tags: string[];
}

export interface CurriculumModule {
  id: string;
  title: string;
  icon: string;
  description: string;
  problems: CurriculumProblem[];
}

export interface CurriculumScheduleItem {
  week: string;
  title: string;
  problems: string[];
  summary: string;
}

export interface CurriculumData {
  modules: CurriculumModule[];
  schedule: CurriculumScheduleItem[];
}
