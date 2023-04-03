import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class UsuarioService {

  apiUrl = environment.baseURL

  constructor(private http: HttpClient, private authService: AuthService) { }

  getUsuarios(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    return this.http.get<any>(`${this.apiUrl}/usuarios/api`, { headers });
  }

  postUsuario(body: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.http.post(`${this.apiUrl}/usuarios/api`, body, {headers})
  }

  putUsuario(body: any): Observable<any> { 
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });   
    return this.http.put(`${this.apiUrl}/usuarios/api`,  body, { headers })
  }

  putContraseña(body: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });   
    return this.http.put(`${this.apiUrl}/usuarios/api/cambiarClave/`, body, { headers })
  }

  getDataUsuario(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    return this.http.get<any>(`${this.apiUrl}/usuarios/api/usuario/`, { headers });
  }

  getReporteUsuario(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    
    return this.http.get<any>(`${this.apiUrl}/usuarios/api/reporteUsuario`, { headers });
  }

  getPuntosUsuario(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
   
    return this.http.get<any>(`${this.apiUrl}/usuarios/api/puntosUsuario/`,{ headers });
  }
}





