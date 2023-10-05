<template><div></div></template>
<script>
import { verifyEmail } from "@/services/authService";
import router from "@/router";
import Swal from 'sweetalert2'
import errorCodes from "@/services/errorCodes.json"
export default {
  mounted() {
    const authenticated = localStorage.getItem("Access_Token")
    if (authenticated) {
      Swal.fire({
        title: 'Are you sure?',
        text: 'A user is already logged in. Are you sure you want to logout and continue the registration?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Continue',
        cancelButtonText: 'No, cancel!',
      }).then((result) => {
        if (result.isConfirmed) {
          localStorage.clear()

          this.verify();
        }
        else {
          Swal.fire(
            'Cancelled',
          )
        }
        this.$router.push({ name: "Home" })
      })
    } else {
      this.verify();
    }
  },
  methods: {
    verify() {
      let param = {
        token: this.$route.params.id,
      };
      verifyEmail(param).then(
        (response) => {
          localStorage.setItem("Email_token",response.data.email_token)
          Swal.fire({
            icon: 'success',
            title: 'Verified',
            text: 'Your email is verified successfully!!',
          })
          this.$router.push({
            name: 'sign-up',
            
          })
        },
        (error) => {
          const errorMessage = errorCodes[error.response.data.error_code] || "Oops.. Some unknown error occurred..!"

          Swal.fire({
            icon: 'error',
            title: 'Failed',
            text: errorMessage,
          })
          router.push("/register-email");
        }
      );

    }
  }
}
</script>
