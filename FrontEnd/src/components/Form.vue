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
      <CRow>
        <StreamingServices></StreamingServices>
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
import  StreamingServices  from './StremingServices.vue';

import { CButton, CRow, CCol} from '@coreui/vue';


export default {
  components: {
    Card,
    CButton,
    CRow,
    CCol,
    StreamingServices
  },
  data() {
    return {
      movies:[],
      genres:[],
      genre:0,
      type:0,
      name:'',
      date:'',
    }
  },
  methods: {
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
    search(){
      //get the generes
      if(this.genre == 0){
        axios.get(
          `https://api.themoviedb.org/3/genre/movie/list?api_key=f9a3efe8c813e81a40a9b661bde37457&language=es-ES`
        ).then(result => this.genres = result.data.genres)
        .catch(error => console.log(error));
      }
      // get elements form the store
      let stars = window.localStorage.movies ? window.localStorage.movies.split(',').map( element => {
        return {
          id: element.split(':')[0],
          stars: element.split(':')[1]
        }
      }) : []

      let streamingServices = window.localStorage.streamingServices ? window.localStorage.streamingServices.split(',') : [];
      let selectedRegion = window.localStorage.region ? window.localStorage.region : "";
      let selectedLanguage = window.localStorage.language ? window.localStorage.language : "";
      
      let post = {
        movies: stars,
        distribuidores: streamingServices,
      };
      axios.post('http://localhost:8080/movies' , 
        post
      ).then( response => {
          console.log(response);
          this.movies = [];
          response.data.forEach( movie => {
            this.movies.push(movie)
            console.log(movie)
          })
      }).catch(error => {
        console.log(error)
      })
    }
  },
  beforeMount(){
    this.search()
  }
}
</script>
<style>

</style>

