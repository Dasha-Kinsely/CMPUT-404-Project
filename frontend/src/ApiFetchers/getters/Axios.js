import axios from "axios";
import {
  allUsers,
  idUsers,
  defaultVisiblePosts,
  idVisiblePosts,
  myFriends,
  myFollowers,
  myFriendRequests,
  currentUser
} from "../globalurl";

export const getCurrentUsers = () => {
  return axios.get(currentUser());
};

export const getAllUsers = () => {
  console.log(axios.get(allUsers()));
  return axios.get(allUsers());
};

export const getIdUsers = uid => {
  console.log(axios.get(idUsers(uid)));
  return axios.get(idUsers(uid));
};

export const getDefaultVisiblePosts = () => {
  return axios.get(defaultVisiblePosts());
};

export const getIdVisiblePosts = uid => {
  return axios.get(idVisiblePosts(uid));
};

export const getMyFriends = uid => {
  return axios.get(myFriends(uid));
};

export const getMyFollowers = uid => {
  return axios.get(myFollowers(uid));
};

export const getMyFriendRequests = () => {
  return axios.get(myFriendRequests);
};
