import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from '../interfaces/user';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  url: string = `${environment.host}:${environment.port}/api/v1/users`

  constructor(private httpClient: HttpClient) { }

  getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json'
    });
  }

  signIn(email: string, password: string): Observable<User> {
    const user_data = {
      email: email,
      password: password
    }
    return this.httpClient.post<User>(this.url, user_data, { headers: this.getHeaders()})
  }

}
