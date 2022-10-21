<template lang="">
  
    <img v-if="movie.poster_path" :src="'https://image.tmdb.org/t/p/w500/'+movie.poster_path"/>
    <img v-else src="/img/poster.jpg"/>

    <h3>{{movie.title}}</h3>

    <h5 v-if="movie.release_date">{{dateFormat(movie.release_date)}}</h5>
    <h5 v-else >Fecha no encontrada</h5>

    <h4>{{movie.vote_average}}/10<span>&#127775;</span></h4>

    <ul v-if="movie.genre_ids">
      <li v-for="movieGenre in genresMovies(movie.genre_ids)">
        {{movieGenre}}
      </li>
    </ul>
    <ul v-else>
      <li v-for="genre in movie.genres">
        {{genre.name}}
      </li>
    </ul>

    <h3 v-if="movie.overview">Synopsis</h3>
    <p>{{movie.overview}}</p>

    <CButton v-if="!isFavorite" class="btn-normal" @Click="changeStorage(movie)" >Añadir a favoritos</CButton>
    <CButton v-if="isFavorite" class="btn-success" @Click="changeStorage(movie)" >Quitar de favoritos</CButton>
</template>

<script>
import poster from '/img/poster.jpg'
import { CButton } from '@coreui/vue';
export default {
  data(){
    return {
      poster: poster, 
      isFavorite: false
    }
  },
  components: {
    CButton
  },
  props: {
    movie: Object,
    genres: Object,
    add: Boolean,
    setDataFromChild:Function
  },
  methods: {
    dateFormat(date) {
      let [yy, mm, dd] = date.split('-')
      return [dd, mm, yy].join('/');
    },
    genresMovies(idGenre){
      let genresArray = [];
      for (let i = 0; i < idGenre.length; i++) {
        for (let j = 0; j < this.genres.length; j++) {
          if (idGenre[i] === this.genres[j].id) {
            genresArray.push(this.genres[j].name)
          }
        }
      }
      return genresArray;
    },
    changeStorage(movie) {
      let storeData = window.localStorage.movies ? window.localStorage.movies.split(',') : [];
      if (storeData.includes(movie.id.toString())) {
        storeData = storeData.filter(id => id !== movie.id.toString());
      } else {
        storeData.push(movie.id.toString());
      }
      window.localStorage.movies = storeData;
      this.isFavorite = !this.isFavorite;
    }
  },
  mounted() {
    let storeData = window.localStorage.movies ? window.localStorage.movies.split(',') : [];
    this.isFavorite = storeData.includes(this.movie.id.toString());
  }
}
</script>
