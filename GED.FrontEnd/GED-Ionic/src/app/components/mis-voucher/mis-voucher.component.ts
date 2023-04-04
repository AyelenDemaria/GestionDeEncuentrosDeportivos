import { Component, OnInit } from '@angular/core';
import { VoucherService } from 'src/app/services/voucher.service';
import { AlertController } from '@ionic/angular';
import { Router } from '@angular/router';


@Component({
  selector: 'app-mis-voucher',
  templateUrl: './mis-voucher.component.html',
  styleUrls: ['./mis-voucher.component.scss'],
})
export class MisVoucherComponent implements OnInit {
  vouchers: any[] = []
  hoy: Date = new Date();

  constructor(
    private voucherService: VoucherService,
    private alertController: AlertController,
    private router: Router
  ) { }

  ngOnInit() {
    console.log(this.hoy)
    this.voucherService.voucherUser().subscribe(
      (data: any[]) => {
        this.vouchers = data;
        console.log(this.vouchers);
      },
      (error: any) => {
        console.log(error);
      }
    );
  }


  estadoUsar(canje, venc) {
    const fechaActual = new Date().toISOString().slice(0, 10);
    const rta = canje === undefined || canje === null && venc >= fechaActual;
    console.log(rta)
    return (rta)
  }

  estadoVencido(canje, venc){
    const fecha = new Date().toISOString().slice(0, 10);
    const fechaActual = new Date(new Date(fecha).getTime() - (24 * 60 * 60 * 1000)).toISOString().slice(0, 10);
    const rta = canje === undefined || canje === null && venc < fechaActual;
    console.log('VENCIDO',rta, venc, fechaActual)
    return (rta)
  }


  usarVoucher(voucher_id: number) {
    this.router.navigate(['/voucher', voucher_id]);
  }

}
