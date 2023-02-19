import { HttpClient } from '@angular/common/http';
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

  getCanchas(): Observable<CanchasDTO[]> {
    return this.httpClient.get<CanchasDTO[]>('https://ayelend.pythonanywhere.com/canchas/api')
  }
}

export interface CanchasDTO{
  nombre: string,
  direccion: string,
  deporte: number 
}