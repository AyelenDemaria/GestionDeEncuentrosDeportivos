import { Component, NgZone, OnInit } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { InscripcionService } from 'src/app/services/inscripcion.service';
import { Router } from '@angular/router';
import { PopoverController } from '@ionic/angular';
import { InscriptosPopoverComponent } from '../inscriptos-popover/inscriptos-popover.component';
import { PartidoService } from 'src/app/services/partido.service';
import { AuthService } from 'src/app/services/auth.service';
import { UsuarioService } from 'src/app/services/usuario.service';


@Component({
  selector: 'app-mis-partidos',
  templateUrl: './mis-partidos.component.html',
  styleUrls: ['./mis-partidos.component.scss'],
})
export class MisPartidosComponent {

  filtro = '';
  partidos: any[] = [];
  perfil: any;


  constructor(
    private alertController: AlertController,
    private inscripcionService: InscripcionService,
    private router: Router,
    private ngZone: NgZone,
    private popoverController: PopoverController,
    private partidoService: PartidoService,
    private authService: AuthService,
    private usuarioService: UsuarioService,

  ) { }

  ionViewDidEnter() {
    this.inscripcionService.getInscripcionesUser().subscribe(
      (data: any[]) => {
        this.partidos = data;
        console.log(this.partidos);
      },
      (error: any) => {
        console.log(error);
      }
    );
    this.perfilUsuario()
  }


  get filteredPartidos() {
    if (this.filtro != "") {
      return this.partidos.filter(x => (x.partido.cancha.deporte.descripcion.toLowerCase() + x.partido.fecha_hora + x.partido.cant_jugadores
        + x.partido.cancha.direccion.toLowerCase() + x.partido.tipo_partido.descripcion.toLowerCase()).
        includes(this.filtro.toLowerCase())).filter(x => x.fecha_hora_baja == null);
    }
    return this.partidos.filter(x => x.fecha_hora_baja == null);
  }


  async mensajeBaja(inscripcionId: number) {
    const alert = await this.alertController.create({
      header: '¿Estas seguro que querés darte de baja del partido?',
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel',
        },
        {
          text: 'OK',
          handler: () => {
            this.bajaInscripcion(inscripcionId);
          },
        },
      ],
    });
    await alert.present();
  }

  bajaInscripcion(inscripcion_id: number) {

    const body = {
      inscripcion_id: inscripcion_id
    }
    this.inscripcionService.bajaInscripcionPartido(body).subscribe(
      (data) => {
        this.mensajeExito()
        // este método actualiza la lista de mis partidos, quitando el id de la inscripción eliminada
        this.updatePartidos(this.partidos.filter(p => p.id !== inscripcion_id));
        this.router.navigateByUrl('/misPartidos');
      },
      (error) => {
        console.log(error)
      });
  }

  async mensajeExito() {
    const alert = await this.alertController.create({
      header: 'Te diste de baja del partido.',
      buttons: ['OK'],
    });
    await alert.present();
  }


  partidoFechaPasada(fecha: string): boolean {
    const fechaPartido = new Date(fecha);
    const fechaActual = new Date();
    return fechaPartido > fechaActual;
  }

  invitar(id_partido: number) {
    this.router.navigate(['/invitar', id_partido]);
  }

  updatePartidos(partidos: any[]) {
    // ngZone le avisa a ionic que una variable cambió
    this.ngZone.run(() => {
      this.partidos = partidos;
    });
  }

  async mostrarInscriptos(idPartido: number) {
    const inscriptos = await this.inscripcionService.getInscriptos(idPartido).toPromise();
    const popover = await this.popoverController.create({
      component: InscriptosPopoverComponent,
      componentProps: {
        inscriptos: inscriptos
      }
    });
    await popover.present();
  }

  async mensajeSuspender(partidoId: number) {
    const alert = await this.alertController.create({
      header: '¿Estas seguro que querés suspender el partido?',
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel',
        },
        {
          text: 'OK',
          handler: () => {
            this.suspender(partidoId);
          },
        },
      ],
    });
    await alert.present();
  }

  suspender(idPartido: number) {
    const body = {
      partido_id: idPartido      
    }
    this.partidoService.suspenderPartido(body).subscribe(
      (data) => {
        this.mensajeExitoSusp()
        // este método actualiza la lista de mis partidos, quitando el id de la inscripción eliminada
        // this.updatePartidos(this.partidos.filter(p => p.id !== inscripcion_id));
        
      },
      (error) => {
        console.log(error)
      });
  } 

  async mensajeExitoSusp() {
    const alert = await this.alertController.create({
      header: 'Partido suspendido',     
    });
    await alert.present();
    window.location.reload(); 
  }

  perfilUsuario() {
    this.usuarioService.getDataUsuario().subscribe(
      (data: any[]) => {
        this.perfil = data;
        console.log(this.perfil);     
      },
      (error) => {
        console.log(error);
      }
    );
  }

  validaCreador(idUser:number): boolean{    
    // console.log(this.perfil?.id,'perfil')
    // console.log(idUser,'creador')
    // console.log(this.perfil?.id  === idUser)
    return this.perfil?.id  === idUser

  }





}
