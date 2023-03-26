import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { AuthService } from './auth.service';


@Injectable({
  providedIn: 'root'
})
export class CanchaService {

  apiUrl = environment.baseURL

  constructor(private http: HttpClient, private authService: AuthService) { }

  getCanchas(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    return this.http.get<any>(`${this.apiUrl}/canchas/api/`, { headers });
  }

  getCanchasByDeporte(idDeporte:number): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword()),
    });
    return this.http.get<any>(`${this.apiUrl}/canchas/api/cancha_deporte?deporte_id=${idDeporte}`, { headers });
  }
}




