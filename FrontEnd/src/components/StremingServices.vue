<template lang="">
    <div class="streaming-services-list">
        <div class="streaming-service">
            <CButton :class="calculateClass('1')" @click="saveStreamingServiceOnLocalStorage('1')">Netflix</CButton>  
        </div>
        <div class="streaming-service">
            <CButton :class="calculateClass('2')" @click="saveStreamingServiceOnLocalStorage('2')">HBO Max</CButton>
        </div>
        <div class="streaming-service">
            <CButton :class="calculateClass('3')" @click="saveStreamingServiceOnLocalStorage('3')">Amazon Prime</CButton>
        </div>
    </div>
</template>
<script>
import { CButton } from '@coreui/vue';
export default {
    components: {
        CButton
    },
    methods: {
    calculateClass(streamingService){
      /* calculates the style of a button if the streaming service is in the local storage */
      let storeData = window.localStorage.streamingServices ? window.localStorage.streamingServices.split(',') : [];
      console.log(storeData)
      if (storeData.includes(streamingService)) {
        return "btn-success"
      }else{
        return "btn-danger"
      }
    },
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