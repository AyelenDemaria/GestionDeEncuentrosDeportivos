import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class InvitacionService {

  constructor(
    private http: HttpClient,
  ) { }

  invitarUsuario(username: string = 'Julieta', password: string = 'Proyecto2022'){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.post<any>('https://ayelend.pythonanywhere.com/invitaciones/api', { headers });
  }

  

  aceptarInvitacion(username: string = 'Julieta', password: string = 'Proyecto2022'){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.put<any>('https://ayelend.pythonanywhere.com/invitaciones/api/aceptarInvitacion/', { headers });
  }



  rechazarInvitacion(username: string = 'Julieta', password: string = 'Proyecto2022'){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.put<any>('https://ayelend.pythonanywhere.com/invitaciones/api/rechazarInvitacion/', { headers });
  }


  invitacionesUser(username: string = 'Julieta', password: string = 'Proyecto2022'){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.get<any>('https://ayelend.pythonanywhere.com/invitaciones/api', { headers });
  }


}
