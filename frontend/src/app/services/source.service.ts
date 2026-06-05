import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Source } from '../interfaces/source';

@Injectable({
  providedIn: 'root'
})
export class SourceService {

  url: string = `http://${environment.host}:${environment.port}/api/v1`;

  constructor(private httpClient: HttpClient) { }

  httpHeaders: HttpHeaders = new HttpHeaders({
    'Content-Type': 'application/json'
  });

  getSources(): Observable<Source[]> {
    return this.httpClient.get<Source[]>(`${this.url}/sources`, { headers: this.httpHeaders });
  }
}
