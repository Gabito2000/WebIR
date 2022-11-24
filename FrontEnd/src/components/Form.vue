<template lang="">
  <div class="form-component">
    <div class='form-container'>
        <!--Género ,Película/Serie , Nombre de pelicula, Fecha-->
        <CRow class="row justify-content-md-center">
          <CCol sm="12" md="2">
            <div class="form-group">
              <label for="genre">Género</label>
              <select class="form-control" id="genre" v-model="genre">
                <option value="0">Todos</option>
                <option v-for="genre in genres" :value="genre.id">{{genre.name}}</option>
              </select>
            </div>
          </CCol>
          <CCol sm="12" md="2">
            <div class="form-group">
              <label for="type">Película/Serie</label>
              <select class="form-control" id="type" v-model="type">
                <option value="0">Todos</option>
                <option value="movie">Película</option>
                <option value="tv">Serie</option>
              </select>
            </div>
          </CCol>
          <CCol sm="12" md="2">
            <div class="form-group">
              <label for="name">Nombre de la película</label>
              <input type="text" class="form-control" id="name" v-model="name" placeholder="Nombre de la película">
            </div>
          </CCol>
          <CCol sm="12" md="2">
            <div class="form-group">
              <label for="date">Fecha</label>
              <input type="date" class="form-control" id="date" v-model="date">
            </div>
          </CCol>
      </CRow>
      <div class='btn-container'>
        <CRow class="row justify-content-md-center" style="margin-top: 10px;margin-bottom: 10px;" >
          <CCol sm="12" md="9">
              <div class="form-group">
                <CButton shape="rounded-pill" type="submit" class="btn btn-primary form-control" @click="search" size="lg">Buscar</CButton>
              </div>
            </CCol>
        </CRow>
      </div>
      <div class='btn-sort-container'>
        <div class='btn-sort' id="goodToBad" @click="setSortGoodBad">
          Top<span>&#8594;</span>
        </div>
        <div class='btn-sort' id="badToGood" @click="setSortGoodBad">
              Flop<span>&#8594;</span>
        </div>
      </div>
    </div>
    <div class="result">
      <div class="cardMovie" v-for="movie in movies" :key="movie.id">
        <Card :movie="movie" :genres="genres" :add="true"/>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import Card from './Card.vue';

import { CButton, CRow, CCol} from '@coreui/vue';

export default {
  components: {
    Card,
    CButton,
    CRow,
    CCol,
  },
  data() {
    return {
      movies:[],
      genres:[],
    }
  },
  methods: {
    getMovies() {
      let stars = window.localStorage.movies ? window.localStorage.movies.split(',').map( element => {
        return {
          id: element.split(':')[0],
          stars: element.split(':')[1]
        }
      }) : []
      let streamingServices = window.localStorage.streamingServices ? window.localStorage.streamingServices.split(',') : [];

      //our server runs on localhost:8080.
      //send the scores and the striming services to the server with a POST request
      axios.post('http://localhost:8080/movies', {
        stars: stars,
        streamingServices: streamingServices
      })

      axios.get(
        `https://api.themoviedb.org/3/genre/movie/list?api_key=f9a3efe8c813e81a40a9b661bde37457&language=es-ES`
      ).then(result => this.genres = result.data.genres)
    },
    setSortGoodBad(e) {
      this.movies.sort((a, b) => {
        if (e.target.id === 'goodToBad') {
          return b.vote_average - a.vote_average;
        } else if (e.target.id === 'badToGood') {
          return a.vote_average - b.vote_average;
        }else {
          return '';
        }
      })
    },
    async search(){
      // get elements form the store
      let stars = window.localStorage.movies ? window.localStorage.movies.split(',').map( element => {
        return {
          id: element.split(':')[0],
          stars: element.split(':')[1]
        }
      }) : []

      let streamingServices = window.localStorage.streamingServices ? window.localStorage.streamingServices.split(',') : [];

      moviesID = await axios.post('http://localhost:8080/movies', {
        stars: stars,
        streamingServices: streamingServices
      })
      if(moviesID.length == 0){
        //do a get request to the API
        axios.get(
          `https://api.themoviedb.org/3/search/movie?api_key=f9a3efe8c813e81a40a9b661bde37457
          &language=${selectedLanguage}
          &region=${selectedRegion}`
        ).then(result => this.movies = result.data.results)
        return 0;
      }
        
      let selectedRegion = window.localStorage.region ? window.localStorage.region : "";
      let selectedLanguage = window.localStorage.language ? window.localStorage.language : "";

      //now search the movies on imdb by id and adds it to the movies
      moviesID.map(movieID =>{
        axios.get(
        `https://api.themoviedb.org/3/search/movie?api_key=f9a3efe8c813e81a40a9b661bde37457
        &language=${selectedLanguage}
        &region=${selectedRegion}
        &query=${movieID}
        `
        ).then(result => this.movies.push(result.data))
      })
    }
  },
  beforeMount(){
    this.getMovies()
  }
}
</script>
<style>

</style>

