export interface CreateReading {
    telescope_id: number;
    az_angle: number;
    el_angle: number;
    health_status: string;
    movement_status: string;
    mag_x: number;
    mag_y: number;
    mag_z: number;
    acc_x: number;
    acc_y: number;
    acc_z: number;
    gyo_x: number;
    gyo_y: number;
    gyo_z: number;
    lon: number;
    lat: number;
    alt: number;
}