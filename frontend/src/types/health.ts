export interface HealthResponse {
  status: string;
  version: string;
  model_loaded: boolean;
  model_file_found: boolean;
}
