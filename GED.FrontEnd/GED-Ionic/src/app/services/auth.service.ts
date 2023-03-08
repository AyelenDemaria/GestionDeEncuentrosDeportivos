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
}

export interface ResponseAuthenticate {
  
}
