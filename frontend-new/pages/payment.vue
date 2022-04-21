<template>
  <div>
    <v-container>
      <v-row justify="center">
        <v-col md="6">
          <v-card tile elevation="0">
            <h2
              class="text-center pt-3"
              style="font-family: playfair display, serif; color: #0285b9"
            >
              Welcome
            </h2>
            <v-card-text
              class="text-center"
              style="
                font-family: playfair display, serif;
                color: #0285b9;
                font-size: 18px;
              "
            >
              Enter your payment id</v-card-text
            >
            <v-container>
              <v-text-field
                outlined
                class="mx-3"
                v-model="paymentid"
                label="Payment Id"
              ></v-text-field>
              <div class="text-center">
                <v-btn
                  color="#0285b9"
                  @click="payment"
                  class="white--text mb-5"
                  width="15em"
                >
                  Sumbit</v-btn
                >
              </div>
            </v-container>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import swal from "sweetalert2";
import { jsPDF } from "jspdf";

export default {
  data() {
    return {
      action: "/bookings/confirm-purchase/",
      paymentid: "",
      rules: {
        required: (value) => !!value || "required.",
      },
    };
  },
  mounted() {
    if (this.$route.query.status) {
      this.status = this.$route.query.status;
    }
    this.initialize();
  },
  methods: {
    initialize() {
      this.paymentid = localStorage.getItem("payment-id");
    },
    async payment() {
      try {
        const response = await this.$axios.patch(this.action + this.paymentid, {
          status: this.status,
        });

        var doc = new jsPDF();
        const lll = response.data.ticket_details;
        const ppp = { ...lll.flight_details, ...lll };
        ppp.flight_details = undefined;
        Object.keys(ppp).forEach((item, i) => {
          doc.text(10, 10 + i * 10, `${item}: ${ppp[item]}`);
          return item, ppp[item];
        });
        // doc.save("ticket.pdf");
        window.open(doc.output("bloburl"));
      } catch (err) {
        swal.fire("error", "please try again later", "error");
      } finally {
        localStorage.removeItem("payment-id");
      }
    },
  },
};
</script>

<style></style>
