<template lang="">
  <div class="user-list-page">
    <Header />
    <h2>Tus Configuraciones</h2>
    <!-- a series of buttons that save on the local storage if it has a netflix hbomax or an other streaming services with core ui icon if it can-->
    <!--The buttons should be separated in a row-->
    <div class="streaming-services-list">
      <div class="streaming-service">
        <CButton :class="calculateClass('Netflix')" @click="saveStreamingServiceOnLocalStorage('Netflix')"><CIcon  name="cib-netflix"/></CButton>  
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('HBO Max')" @click="saveStreamingServiceOnLocalStorage('HBO Max')">HBO Max</CButton>
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('Disney Plus')" @click="saveStreamingServiceOnLocalStorage('Disney Plus')">Disney Plus</CButton>
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('Amazon Prime')" @click="saveStreamingServiceOnLocalStorage('Amazon Prime')"><CIcon  name="cib-amazon"/></CButton>
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('Apple TV Plus')" @click="saveStreamingServiceOnLocalStorage('Apple TV Plus')">Apple TV Plus</CButton>
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('Hulu')" @click="saveStreamingServiceOnLocalStorage('Hulu')">Hulu</CButton>
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('Crunchyroll')" @click="saveStreamingServiceOnLocalStorage('Crunchyroll')"><CIcon  name="cib-crunchyroll"/></CButton>
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('Peacock')" @click="saveStreamingServiceOnLocalStorage('Peacock')">Peacock</CButton>
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('Paramount Plus')" @click="saveStreamingServiceOnLocalStorage('Paramount Plus')">Paramount Plus</CButton>
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('Starz')" @click="saveStreamingServiceOnLocalStorage('Starz')">Starz</CButton>
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('Showtime')" @click="saveStreamingServiceOnLocalStorage('Showtime')">Showtime</CButton>
      </div>
      <div class="streaming-service">
        <CButton :class="calculateClass('Youtube Premium')" @click="saveStreamingServiceOnLocalStorage('Youtube Premium')"><CIcon  name="cib-youtube"/></CButton>
      </div>
    </div>
    <!--
      CFormSelect the region of the user when change save it on the local storage
    -->
    <CRow class="row justify-content-md-center">
      <CCol sm="12" md="3" >
        <h3>Región</h3>
        <CFormSelect v-model="selectedRegion" :options="regionOptions" @change="saveRegionOnLocalStorage"/>
      </CCol>
      <CCol sm="12" md="3" >
        <h3>Idioma</h3>
        <CFormSelect v-model="language" :options="languageOptions" @change="saveLanguageOnLocalStorage"/>
      </CCol>
    </CRow>

    <!--
      CFormSelect the language of the user
    -->
</div>
</template>

<script>
import Header from "../components/Header.vue";
import { CButton, CFormSelect, CRow, CCol} from '@coreui/vue';

export default {
  data() {
    return {
      streamingServices: [],
      /* iso 3166-1 */
      /* latam, europe and usa */
      regionOptions: [
        { value: "", label: "Todas" },
        { value: "UR", label: "Uruguay" },
        { value: "AR", label: "Argentina" },
        { value: "BR", label: "Brasil" },
        { value: "CL", label: "Chile" },
        { value: "CO", label: "Colombia" },
        { value: "MX", label: "Mexico" },
        { value: "PE", label: "Peru" },
        { value: "VE", label: "Venezuela" },
        { value: "ES", label: "España" },
        { value: "FR", label: "Francia" },
        { value: "GB", label: "Reino Unido" },
        { value: "US", label: "Estados Unidos" },
      ],
      selectedRegion: "",
      languageOptions: [
        { value: "es", label: "Español" },
        { value: "en", label: "English" },
      ],
      selectedLanguage: "es",
    }
  },
  components: {
    Header,
    CButton,
    CFormSelect,
    CRow,
    CCol,
  },
  methods: {
    reRender() {
      this.$forceUpdate();
    },
    saveStreamingServiceOnLocalStorage(streamingService){
      
      /*saves or removes from the local storage the streaming service */
      let storeData = window.localStorage.streamingServices ? window.localStorage.streamingServices.split(',') : [];
      if (!storeData.includes(streamingService)) {
        storeData.push(streamingService)
        window.localStorage.streamingServices = storeData
        this.streamingServices = storeData;
      }else{
        let indexMovie = storeData.indexOf(streamingService);
        if(indexMovie != -1){
          storeData.splice(indexMovie, 1);
          window.localStorage.streamingServices = storeData;
          this.streamingServices = storeData;
        }
      }
      this.reRender();
    },
    calculateClass(streamingService){
      /* calculates the style of a button if the streaming service is in the local storage */
      let storeData = window.localStorage.streamingServices ? window.localStorage.streamingServices.split(',') : [];
      if (storeData.includes(streamingService)) {
        return "btn-success"
      }else{
        return "btn-danger"
      }
    },
    saveRegionOnLocalStorage(event){
      /* saves the region on the local storage */
      this.selectedRegion = event.target.value;
      window.localStorage.region = event.target.value;
    },
    saveLanguageOnLocalStorage(event){
      /* saves the language on the local storage */
      this.selectedLanguage = event.target.value;
      window.localStorage.language = event.target.value;
    }
  },
  mounted(){
    /* gets the streaming services from the local storage */
    let storeData = window.localStorage.streamingServices ? window.localStorage.streamingServices.split(',') : [];
    this.streamingServices = storeData;
    /* gets the region from the local storage */
    this.selectedRegion = window.localStorage.region ? window.localStorage.region : "";
    /* gets the language from the local storage */
    this.selectedLanguage = window.localStorage.language ? window.localStorage.language : "";

  }
}
</script>
<style>
.form-select{
  width: 100%;
  margin-top: 10px;
  margin-bottom: 10px;
  background: rgba(0, 0, 0, 0.3);
  color: #fff;
  text-shadow: 0 1px 0 rgba(0, 0, 0, 0.4);
}
.streaming-services-list {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  align-content: center;
}
.streaming-service {
  margin: 0.5rem;
  padding: 0.5rem;
  border-radius: 0.25rem;
}
</style>