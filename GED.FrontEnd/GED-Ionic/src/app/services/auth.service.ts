import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  apiUrl = environment.baseURL;

  constructor(private http: HttpClient) { }

  authenticate(username: string, password: string): Observable<any> {
    const body = {
      username: username,
      password: password
    }
    sessionStorage.setItem('username', username);
    sessionStorage.setItem('password', password); //TODO: hashear o cifrar
    return this.http.post(`${this.apiUrl}/usuarios/api/login/`, body);
  }


  logout(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.getUsername() + ':' + this.getPassword())
    });
    return this.http.get<any>(`${this.apiUrl}/usuarios/api/logout/`, { headers });
  }

  getUsername(): string {
    return sessionStorage.getItem('username');
  }

  getPassword(): string {
    //TODO: descifrar/deshashear
    return sessionStorage.getItem('password');
  }

}

export interface ResponseAuthenticate {
  
}
