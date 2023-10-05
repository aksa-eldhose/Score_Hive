<template><div></div>
</template>
<script>
import { sendToken } from "@/services/authService";
import errorCodes from "@/services/errorCodes.json";
import Swal from "sweetalert2";
export default {
  created() {
    let param = {
      user_id: this.$route.params.id,
      token: this.$route.params.token,
    };
    sendToken(param).then(
      (response) => {
        Swal.fire({
          position: "center",
          icon: "success",
          text: "Your email is verified successfully",
          showConfirmButton: false,
          timer: 1500,
        });
        localStorage.setItem("email", response.data.email);
        this.$router.push({
          name: "ResetPassword",
        });
      },
      (error) => {
        const errorMessage =
          errorCodes[error.response.data.error_code] ||
          "Oops.. Some unknown error occurred..!";
        this.$router.push({
          name: "SignIn",
        });
        Swal.fire({
          position: "center",
          icon: "error",
          text: errorMessage,
          showConfirmButton: false,
          timer: 1000,
        });
      }
    );
  },
};
</script>
