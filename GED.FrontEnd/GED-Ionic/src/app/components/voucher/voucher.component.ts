import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { VoucherService } from 'src/app/services/voucher.service';
import { Router } from '@angular/router';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-voucher',
  templateUrl: './voucher.component.html',
  styleUrls: ['./voucher.component.scss'],
})
export class VoucherComponent {
  voucher_id: number;
  voucher: any

  constructor(
    private route: ActivatedRoute,
    private VoucherService: VoucherService,
    private router: Router,
    private alertController: AlertController,
  ) { }

  ionViewDidEnter() {
    this.route.params.subscribe(params => {
      this.voucher_id = params['voucher_id']; 
      console.log(this.voucher_id)     
    });

    this.obtenerVoucher(this.voucher_id)
  }


  obtenerVoucher(voucher_id:number){
    this.VoucherService.getVoucherById(voucher_id).subscribe(response => {
      this.voucher = response;
      console.log(response);
    });
  }

  usarVoucher(){
    const body = {
      voucher_id : this.voucher_id
    }
    this.VoucherService.usarVoucher(body).subscribe(
      (data) => {
        console.log(data)
        const codigo = data.codigo; 
        this.mensajeExito(codigo)
        this.router.navigate(['/misVoucher'])
        this.router.navigateByUrl('/misVoucher', { skipLocationChange: true }).then(() => {
          this.router.navigate(['/misVoucher']);
        });       
      },
      (error) => {
        console.log(error)
      }
    );        
  }



    async mensajeExito(codigo:number) {
      const alert = await this.alertController.create({
        subHeader: `${codigo}`,
        message: 'Este es tu código de uso, debes mostrarlo en la cancha.',   
     
        buttons: ['OK'],
      });
      await alert.present();
  }


  cancelar(){
   this.router.navigateByUrl('/misVoucher', { replaceUrl: true });
  }


 

}
