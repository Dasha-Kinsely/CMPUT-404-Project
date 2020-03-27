import React, { Fragment } from "react";
import { Segment, List, Grid, Header, Divider } from "semantic-ui-react";

export default () => (
  <Fragment>
    <Grid.Row style={{ height: "100px" }}></Grid.Row>
    <Segment
      inverted
      vertical
      style={{ margin: "15em 0em 0em", padding: "0em 0em" }}
    >
      <Grid.Row>
        <br />
      </Grid.Row>
      <Header as="h2" textAlign="center">
        About Hindle's Wonderland
      </Header>
      <Grid divided inverted stackable>
        <Grid.Column width={3}></Grid.Column>
        <Grid.Column width={2}>
          <Header inverted as="h4" content="Dashboard" />
          <List link inverted>
            <List.Item as="a">Link One</List.Item>
            <List.Item as="a">Link Two</List.Item>
          </List>
        </Grid.Column>
        <Grid.Column width={2}>
          <Header inverted as="h4" content="Category" />
          <List link inverted>
            <List.Item as="a">Link One</List.Item>
            <List.Item as="a">Link Two</List.Item>
          </List>
        </Grid.Column>
        <Grid.Column width={2}>
          <Header inverted as="h4" content="Trendings" />
          <List link inverted>
            <List.Item as="a">Link One</List.Item>
            <List.Item as="a">Link Two</List.Item>
          </List>
        </Grid.Column>
        <Grid.Column width={4}>
          <Header inverted as="h4" content="An UAlberta-Based Company" />
          <p>
            Proudly Designed and Developed by UAlberta CS Students. Made with
            Uttermost Efforts and Dedication for Professor Hindle.
          </p>
        </Grid.Column>
        <Grid.Column width={3}></Grid.Column>
      </Grid>
      <Divider inverted section />
      <Grid>
        <Grid.Column width={3}></Grid.Column>
        <Grid.Column width={10}>
          <List horizontal inverted divided link size="small">
            <List.Item as="a" href="/misc/sitemap">
              Site Map
            </List.Item>
            <List.Item as="a" href="mailto:yuntai@ualberta.ca">
              Contact Us
            </List.Item>
            <List.Item as="a" href="/misc/terms">
              Terms and Conditions
            </List.Item>
            <List.Item as="a" href="/misc/policy">
              Privacy Policy
            </List.Item>
          </List>
        </Grid.Column>
        <Grid.Column width={3}></Grid.Column>
        <Divider inverted section />
      </Grid>
    </Segment>
  </Fragment>
);
