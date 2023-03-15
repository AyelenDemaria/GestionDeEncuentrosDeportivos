import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class VoucherService {

  constructor(
    private http: HttpClient,
  ) { }

  crearVoucher(username: string = 'Julieta', password: string = 'Proyecto2022'){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.post<any>('https://ayelend.pythonanywhere.com/vouchers/api', { headers });
  }


  usarVoucher(body: string, username: string = 'Julieta', password: string = 'Proyecto2022'){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    const options = {
      headers: headers,
      params: body
    }
    return this.http.put<any>('https://ayelend.pythonanywhere.com/vouchers/api', options);
  }


  voucherUser(username: string = 'Julieta', password: string = 'Proyecto2022'){
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Basic ' + btoa(username + ':' + password)
    });
    return this.http.get<any>('https://ayelend.pythonanywhere.com/vouchers/api', { headers });
  }

}
