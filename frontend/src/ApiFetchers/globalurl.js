import "react";

//Set localhost addresses.
var location = window.location;
var protocol = location.protocol;
var host = protocol.concat(`//${location.host}/api/`).replace("3000", "8000");

//The address of each url is specified in the return statement, they are expected to match the backend services.

export const defaultVisiblePosts = () => {
  return `${host}author/posts`;
};

export const idVisiblePosts = uid => {
  return `${host}author/${uid}/posts`;
};

export const myFriends = uid => {
  return `${host}friends/${uid}/`;
};

export const myFollowers = uid => {
  return `${host}followers/${uid}/`;
};

export const myFriendRequests = () => {
  return `${host}friendrequests/`;
};

export const acceptFriendRequests = uid => {
  return `${host}friendrequests/${uid}/accept`;
};

export const rejectFriendRequests = uid => {
  return `${host}friendrequests/${uid}/reject`;
};

export const deleteFriendRequests = uid => {
  return `${host}friendrequests/${uid}/delete`;
};

export const allPosts = () => {
  return `${host}posts/`;
};

export const idPosts = id => {
  return `${host}posts/${id}/`;
};

export const allUsers = () => {
  return `${host}users/`;
};

export const idUsers = uid => {
  return `${host}users/${uid}/`;
};
