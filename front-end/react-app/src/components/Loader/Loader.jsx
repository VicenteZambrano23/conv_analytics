import styles from './Loader.module.css'

export function Loader({isGraph}){
    return(<div>
        {isGraph ? 
            (<div className = {styles.LoaderWrapper}>
            <div className = {styles.loader}/>
        </div>) : (<div className = {styles.LoaderWrapperCenter}>
            <div className = {styles.loader}/>
        </div>)
    }</div>
        
        
    )
}