import "react";

//Set localhost addresses.
var location = window.location;
var protocol = location.protocol;
var host = protocol.concat(`//${location.host}/api/`).replace("3000", "8000");
var althost = protocol
  .concat(`//${location.host}/auth/`)
  .replace("3000", "8000");

//The address of each url is specified in the return statement, they are expected to match the backend services.
export const authRegister = () => {
  return `${althost}register`;
};
//POST: add a new user to db => {email, username, password}

export const authLogin = () => {
  return `${host}login`;
};
//POST: log user in => {email, username, password}

export const authLogout = () => {
  return `${althost}logout`;
};
//POST: clear csrf and logout => {}

export const currentUser = () => {
  return `${host}currentuser/`;
};
//GET: returns current user

export const defaultVisiblePosts = () => {
  return `${host}author/posts`;
};
//GET: return all posts visible to currently authenticated author

export const idVisiblePosts = uid => {
  return `${host}author/${uid}/posts`;
};
//GET: return all posts of author with the given {uid}

export const myFriends = uid => {
  return `${host}author/${uid}/friends/`;
};
//GET: get all friends associated with {uid} => basic_auth, {uid}
export const myFollowers = uid => {
  return `${host}author/${uid}/followers/`;
};
//GET: return all authors following {uid}
export const myFriendRequests = uid => {
  return `${host}author/${uid}/friendrequests/`;
};
//GET: return all types of friend requests => basic_auth, {uid}
export const allFriendRequests = () => {
  return `${host}friendrequests/`;
};
//GET: return all records of friendrequests (of any authors)
//POST: makes new follow request to be approved => basic_auth, {followee_url, follower_url}

export const acceptFriendRequests = uid => {
  return `${host}friendrequests/${uid}/accept`;
};
//PUT: accept friend request => basic_auth, {request_id}
export const rejectFriendRequests = uid => {
  return `${host}friendrequests/${uid}/reject`;
};
//PUT: reject friend request => basic_auth, {request_id}
export const deleteFriendRequests = uid => {
  return `${host}friendrequests/${uid}/delete`;
};
//DELETE: delete a friend => basic_auth, {request_id}
export const allPosts = () => {
  return `${host}posts/`;
};
//GET: return all 'public' posts.
//POST: create new post => {content, origin_post, text_type, visibility, unlist}

export const idPosts = id => {
  return `${host}posts/${id}/`;
};
//GET: return the post with {pid} if it is viewable to authenticated user
//PUT: updates the post with {pid}
//DELETE: delete a post with {pid}
export const allUsers = () => {
  return `${host}author/`;
};
//GET: all of the users
//POST: register a new user

export const idUsers = uid => {
  return `${host}users/${uid}/`;
};
//GET: return the user with {uid}
//PUT: update the user with {uid}
//DELETE: delete the user with {uid}
