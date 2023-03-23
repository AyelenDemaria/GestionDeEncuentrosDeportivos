import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class InscripcionService {

  apiUrl = environment.baseURL;

  constructor(private http: HttpClient, private authService: AuthService) { }

  crearInscripcionPartido(partido_id: number) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    const body = {
      partido_id: partido_id,
    }
    return this.http.post<any>(`${this.apiUrl}/inscripciones/api/${partido_id}/`, body, {headers});
  }

  bajaInscripcionPartido(body: string, inscripcionId: number) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    const options = {
      headers: headers,
      params: { body, inscripcionId: inscripcionId }
    }
    return this.http.put<any>(`${this.apiUrl}/inscripciones/api/`, options);
  }

  getInscripcionesUser(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    return this.http.get<any>(`${this.apiUrl}/inscripciones/api/inscripcion/`,{ headers });
  }
}