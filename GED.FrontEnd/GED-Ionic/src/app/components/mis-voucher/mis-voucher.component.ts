import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-mis-voucher',
  templateUrl: './mis-voucher.component.html',
  styleUrls: ['./mis-voucher.component.scss'],
})
export class MisVoucherComponent implements OnInit {

vouchers: any[] = [
  {nombre: 'Cancha SRL',
   direccion:'Alvear 2040',
   deporte: 'Tenis',
   fechaEmision:'06-02-23',
   fechaVenc:'30-06-23' },

   {nombre: 'Cancha 5',
   direccion:'Rioja 683',
   deporte: 'Futbol',
   fechaEmision:'15-01-23',
   fechaVenc:'30-05-23' },
] ;


  constructor() {
   
   }

  ngOnInit() {}

}
