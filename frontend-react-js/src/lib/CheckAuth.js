// Auth using Amazon Cognito
import { Auth } from 'aws-amplify';

export default async function checkAuth(setUser){
  // console.log('checkAuth')
  // // [TODO] Authentication
  // if (Cookies.get('user.logged_in')) {
  //   setUser({
  //     display_name: Cookies.get('user.name'),
  //     handle: Cookies.get('user.username')
  //   })
  // }
  Auth.currentAuthenticatedUser({
    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((user) => {
    console.log('user',user);
    return Auth.currentAuthenticatedUser()
  }).then((cognito_user) => {
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
  })
  .catch((err) => console.log(err));
};
