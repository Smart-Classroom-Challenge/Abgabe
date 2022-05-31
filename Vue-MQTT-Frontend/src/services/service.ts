import http from '~/http-commmon'
class api {
  getClassrooms(token: any): Promise<any> {
    return http.get('/Classrooms/', { headers: { Accept: 'application/json', Authorization: `Bearer ${token}` } })
  }

  create_classroom(token: any, data: any): Promise<any> {
    return http.post('/Classrooms/', data, { headers: { Accept: 'application/json', Authorization: `Bearer ${token}` } })
  }

  create_station(token: any, data: any): Promise<any> {
    return http.post('/MeasurementStations/', data, { headers: { Accept: 'application/json', Authorization: `Bearer ${token}` } })
  }

  get(data: any): Promise<any> {
    return http.post(`/tutorials/${id}`, data)
  }

  check_jwt(token: any): Promise<any> {
    return http.get('/Classrooms/', { headers: { Accept: 'application/json', Authorization: `Bearer ${token}` } })
  }

  create(data: any): Promise<any> {
    return http.post('/token/', data)
  }

  update(id: any, data: any): Promise<any> {
    return http.put(`/tutorials/${id}`, data)
  }

  delete(id: any): Promise<any> {
    return http.delete(`/tutorials/${id}`)
  }

  deleteAll(): Promise<any> {
    return http.delete('/tutorials')
  }

  findByTitle(title: string): Promise<any> {
    return http.get(`/tutorials?title=${title}`)
  }
}
export default new api()
