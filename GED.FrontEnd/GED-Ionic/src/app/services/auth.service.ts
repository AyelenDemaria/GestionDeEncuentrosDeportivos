import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class AuthService {

  apiUrl = environment.baseURL

  constructor(
    private httpClient: HttpClient,
  ) { }

  authenticate(username: string, password: string): Observable<any> {
    const body = {
      username: username,
      password: password
    }
    return this.httpClient.post('https://ayelend.pythonanywhere.com/usuarios/api/login/', body);
  }


  logout(username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.httpClient.get<any>('https://ayelend.pythonanywhere.com/usuarios/api/logout/ ', { headers });
  }


}

export interface ResponseAuthenticate {
  
}
