import { Injectable } from '@angular/core';
import { Observable, ObservedValuesFromArray } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { LikePayload } from '../models/like.payload';

@Injectable({
  providedIn: 'root'
})
export class SwipeService {

  constructor(private http: HttpClient) { }

  getPersonsByZodiac(token: string): Promise<any> {
    return fetch('http://localhost:8000/get_persons_by_zodiac?token='+token).then(response => response.json());
  }
  likePerson(likePayload: LikePayload, token: string): Observable<any>{
      return this.http.post('http://localhost:8000/like?token=' + token, likePayload);
  }
}