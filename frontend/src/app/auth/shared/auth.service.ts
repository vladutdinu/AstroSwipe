import { Injectable } from '@angular/core';
import { FirstRegisterPayload } from '../shared/first-register.payload'
import { SecondRegisterPayload } from '../shared/second-register.payload'
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  signup(firstRegisterPayload: FirstRegisterPayload ): Observable<any> {
    return this.http.post('http://localhost:8000/register_step1', firstRegisterPayload);
  }

  register(secondRegisterPayload: SecondRegisterPayload ): Observable<any> {
    return this.http.post('http://localhost:8000/register_step2', secondRegisterPayload);
  }
}