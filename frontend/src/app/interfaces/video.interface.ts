export interface Video {
  id: number;
  title: string;
  description: string;
  video_file: string;
  hls_playlist: string;
  thumbnail: string;
  created_at: string;
  categories: string[];
}
