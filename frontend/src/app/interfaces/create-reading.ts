export interface CreateReading {
    telescope_id: number;
    az_angle: number;
    el_angle: number;
    health_status: string;
    movement_status: string;
}