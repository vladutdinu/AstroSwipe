import { Injectable } from '@angular/core';
import { Observable, ObservedValuesFromArray } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { LikePayload } from '../models/like.payload';
import { ProfilePayload } from '../models/profile.payload';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  constructor(private http: HttpClient) { }

  updateBio(profilePayload: ProfilePayload, token: string): Observable<any> {
    return this.http.post('http://localhost:8000/update_bio?token='+token, profilePayload);
  }
  getInfo(token: string): Promise<any>{
    return fetch('http://localhost:8000/get_profile_data?token='+token).then(response => response.json());
  }
  deleteProfile(token: string): Observable<any>{
    return this.http.delete('http://localhost:8000/delete_profile?token='+token);
  }
}