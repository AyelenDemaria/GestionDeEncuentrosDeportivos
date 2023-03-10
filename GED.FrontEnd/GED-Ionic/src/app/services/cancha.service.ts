import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CanchaService {

  apiUrl = environment.baseURL

  constructor(
    private httpClient: HttpClient
  ) { }

  getCanchas(username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.httpClient.get<any>('https://ayelend.pythonanywhere.com/canchas/api/', { headers });
  }

  getCanchasByDeporte(deporte_id: number, username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    const url = `https://ayelend.pythonanywhere.com/canchas/api/cancha_deporte?deporte_id=${deporte_id}`;
    console.log(url)

    return this.httpClient.get<any>(url, { headers });
    // return this.httpClient.get<any>('https://ayelend.pythonanywhere.com/canchas/api/cancha_deporte/',{ headers });
  }
}




