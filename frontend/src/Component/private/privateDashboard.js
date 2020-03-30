import React, { useState, useEffect } from "react";
import { getCurrentUsers } from "../../ApiFetchers/getters/Axios";

const PrivateDashboard = () => {
  const [current, setCurrent] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    const profileList = async () => {
      setIsLoading(true);
      try {
        let followersFetcher = await getCurrentUsers(); //get data from api's url
        console.log(followersFetcher);
        setCurrent(followersFetcher);
      } catch (error) {
        console.log(error);
      }
      setIsLoading(false);
    };
    profileList();
  }, []);
  return <div>{isLoading ? <p>Loading</p> : <p>{current}</p>}</div>;
};
export default PrivateDashboard;
