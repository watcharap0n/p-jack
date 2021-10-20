{% extends 'layout.html' %}
{% block content %}

<v-container>

<br>
<v-row>
  <v-icon
      large
      color="blue lighten-1"
      style="margin-bottom: 20px"
  >
    mdi-robot
  </v-icon>
  &nbsp;&nbsp;
  <h2>
    Hydroponic IoT
  </h2>
</v-row>
<v-divider></v-divider>

<v-switch
    v-model="switch1"
    color="success"
    :label="`Automation IoT: ${switch1 === true ? 'On': 'Off'}`"
></v-switch>
<v-responsive
    class="overflow-y-auto"
    height="800px"
>
  <v-card v-for="(v,i) in esp" :key="i" :loading="!spinCard">
    <v-card-title>[[v.elc]]</v-card-title>
    <v-card-text>
      <div class="my-4 text-subtitle-1" :hidden="switch1">
        สถานะปัจจุบัน: [[v.description]]
      </div>
      <div class="my-4 text-subtitle-1" v-if="switch1">
        สถานะปัจจุบัน: กำลังทำงานออโต้
      </div>
      <v-row>
        <v-col cols="6">
          <v-btn
              :hidden="hiddenCard"
              class="mx-2"
              fab
              dark
              large
              :color="v.status === true ? 'success' : 'error'"
              @click="ticket({'id': i, 'status': v.status})"
          >
            <v-icon dark>
              mdi-power
            </v-icon>
          </v-btn>
          <v-row
              :hidden="!switch1"
          >
            <v-progress-circular
                :size="50"
                color="primary"
                indeterminate
            ></v-progress-circular>
            &nbsp;&nbsp;
          </v-row>
        </v-col>
        <v-col cols="6">
          <v-row>
            <v-avatar>
              <img
                  :src="user.img"
                  alt="NaN"
              >
            </v-avatar>
            <h6 style="margin-left: 10px; margin-top: 10px">User: [[user.display_name]]</h6>
          </v-row>

          <div class="my-4 text-subtitle-1">
            [[v.sensor]]
          </div>
        </v-col>

      </v-row>
    </v-card-text>
  </v-card>
</v-responsive>


<v-overlay :value="!spinCard">
  <v-progress-circular
      indeterminate
      size="64"
  ></v-progress-circular>
</v-overlay>

</v-container>

{% block script %}
<script src="/static/js/index.js"></script>
{% endblock %}

{%endblock%}