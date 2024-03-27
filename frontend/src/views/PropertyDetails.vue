<template>
  <button class="home-button" @click="goHome">Go Home</button>
  <div class="property-details">
    <h2>Property Details</h2>
    <div v-if="property" class="details">
      <div class="text-details">
        <p><strong>Longitude:</strong> {{ property.longitude }}</p>
        <p><strong>Latitude:</strong> {{ property.latitude }}</p>
        <p><strong>Class Description:</strong> {{ property.class_description }}</p>
        <p><strong>Estimated Market Value:</strong> ${{ property.estimated_market_value }}</p>
        <p><strong>Building Use:</strong> {{ property.bldg_use }}</p>
        <p><strong>Building Square Feet:</strong> {{ property.building_sq_ft }} sqft</p>
        <p><strong>Zip Code:</strong> {{ property.zip }}</p>
        <p><strong>Land Square Feet:</strong> {{ property.land_sq_ft }} sqft</p>
        <p><strong>Age:</strong> {{ property.age }}</p>
        <p><strong>Number of Units:</strong> {{ property.units_tot }}</p>
        <p><strong>Fireplaces:</strong> {{ property.fireplace }}</p>
        <p><strong>Air Conditioning:</strong> {{ property.ac ? 'Yes' : 'No' }}</p>
        
        <p>{{ property.full_address }}</p>
      </div>
      <div class="map-container" v-if="property.latitude && property.longitude">
        <l-map :zoom="13" :center="[property.latitude, property.longitude]" style="height: 400px">
          <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"></l-tile-layer>
          <l-marker :lat-lng="[property.latitude, property.longitude]"></l-marker>
        </l-map>
      </div>
    </div>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from 'vue3-leaflet';
import 'leaflet/dist/leaflet.css';
import http from '@/http';

export default {
  name: 'PropertyDetails',
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data() {
    return {
      property: null,
    };
  },
  methods: {
    goHome() {
      this.$router.push('/home');
    }
  },
  async created() {
    try {
      const response = await http.get(`properties/${this.$route.params.id}`);
      this.property = response.data;
    } catch (error) {
      console.error("Failed to fetch property details:", error);
    }
  },
};
</script>

<style scoped>
.property-details {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.details {
  display: flex;
  flex-direction: column;
}

.text-details, .map-container {
  margin-bottom: 20px;
}

.map-container {
  margin-top: 20px;
  border: 2px solid #007bff; 
  border-radius: 8px;
  overflow: hidden;
  height: 400px; /* Adjusted to match inline style */
}

.home-button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.home-button:hover {
  background-color: #0056b3;
}
</style>
