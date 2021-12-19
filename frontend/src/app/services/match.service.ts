import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { LikePayload } from '../models/like.payload';

@Injectable({
    providedIn: 'root'
})
export class MatchService {

    constructor(private http: HttpClient) { }

    getMatches(token: string): Promise<any> {
        return fetch('http://localhost:8000/get_matches?token=' + token).then(response => response.json());
    }
    unmatch(likePayload: LikePayload, token: string): Observable<any> {
        return this.http.post('http://localhost:8000/unmatch?token=' + token, likePayload);
    }
}