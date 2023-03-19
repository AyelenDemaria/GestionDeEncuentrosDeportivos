import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PartidoService {

  apiUrl = environment.baseURL

  constructor(
    private http: HttpClient,
  ) { }

  getPartidos(username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.get<any>('https://ayelend.pythonanywhere.com/partidos/api', { headers });
  }

  getTiposPartidos(username: string = 'Julieta', password: string = 'Proyecto2022'): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.get<any>('https://ayelend.pythonanywhere.com/tipos_partidos/api', { headers });
  }

  postPartido( body:any):Observable<any> { 
    
    return this.http.post('https://ayelend.pythonanywhere.com/partidos/api', body)
  }

  cantidadInscriptosPartido(username: string = 'Julieta', password: string = 'Proyecto2022'){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.get<any>('https://ayelend.pythonanywhere.com/partidos/api/inscriptos/', { headers });
  }

}
