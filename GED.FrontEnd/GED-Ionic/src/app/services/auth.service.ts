import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  
  apiUrl = environment.baseURL

  constructor(
    private httpClient: HttpClient
  ) { }

  getCanchas(): Observable<any> {
    return this.httpClient.get<any>('https://ayelend.pythonanywhere.com/canchas/api')
  }
}


