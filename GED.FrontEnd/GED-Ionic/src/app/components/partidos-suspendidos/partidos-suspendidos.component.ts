import { Component, NgZone, OnInit } from '@angular/core';
import { InscripcionService } from 'src/app/services/inscripcion.service';

@Component({
  selector: 'app-partidos-suspendidos',
  templateUrl: './partidos-suspendidos.component.html',
  styleUrls: ['./partidos-suspendidos.component.scss'],
})
export class PartidosSuspendidosComponent implements OnInit {

  partidos: any[] = [];
  todasLeidas = false


  constructor(
    private inscripcionService: InscripcionService,
    private ngZone: NgZone,
  ) { }

  ngOnInit() {
    this.getPartidos()
  }

  getPartidos(){ 
    this.inscripcionService.getPartidosSuspendidos().subscribe(
      (data: any[]) => {
        this.partidos = data;
        this.todasLeidas= this.partidos.length ===0
        console.log(this.partidos);
      },
      (error: any) => {
        console.log(error);
      }
    );
  }

  marcarLeido(inscripcion_id: number){
    const body = {
      inscripcion_id: inscripcion_id
    }
    this.inscripcionService.setNotificado(body).subscribe(
      (data) => {        console.log('entra')
        // este método actualiza la lista de mis partidos, quitando el id de la inscripción eliminada
        this.updatePartidos(this.partidos.filter(p => p.id !== inscripcion_id));       
      },
      (error) => {
        console.log(error)
      });  
  }

  updatePartidos(partidos: any[]) {
    // ngZone le avisa a ionic que una variable cambió
    this.ngZone.run(() => {
      this.partidos = partidos;
    });
  }

}
