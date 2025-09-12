import { CreateReading } from "./create-reading";

export interface Reading extends CreateReading {
    id: number;
    created_at: Date;
}

