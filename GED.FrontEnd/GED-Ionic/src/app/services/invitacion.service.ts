import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InvitacionService {

  apiUrl = environment.baseURL;

  constructor(private http: HttpClient, private authService: AuthService) { }

  invitarUsuario(body:any):Observable<any> {  
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });  
    return this.http.post<any>(`${this.apiUrl}/invitaciones/api`, body, { headers });
  }

  aceptarInvitacion(body:any){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    return this.http.put<any>(`${this.apiUrl}/invitaciones/api/aceptarInvitacion/`, body, { headers });
  }

  rechazarInvitacion(body:any){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    return this.http.put<any>(`${this.apiUrl}/invitaciones/api/rechazarInvitacion/`, body, { headers });
  }

  invitacionesUser(){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(this.authService.getUsername() + ':' + this.authService.getPassword())
    });
    return this.http.get<any>(`${this.apiUrl}/invitaciones/api`, { headers });
  }


}
