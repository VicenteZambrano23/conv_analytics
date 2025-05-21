import styles from './GraphLoader.module.css'

export function GraphLoader(){
    return(
        <div className = {styles.LoaderWrapper}>
            <div className = {styles.loader}/>
        </div>
    )
}